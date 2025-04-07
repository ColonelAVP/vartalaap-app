from .forms import CustomUserCreationForm
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Answer, AnswerLike, QuestionLike, Comment, CustomUser
from django.contrib.auth.decorators import login_required
from .forms import AnswerForm, QuestionForm, CommentForm
from django.db.models import Count
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponseForbidden
from django.urls import reverse

User = get_user_model()

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("login_page")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/register.html", {"form": form})


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Add custom user data to token response
        data.update(
            {
                "user_id": self.user.id,
                "username": self.user.username,
                "email": self.user.email,
            }
        )

        return data


class LoginAPIView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect(request.GET.get("next", "/dashboard/"))
        else:
            return render(
                request, "registration/login.html", {"error": "Invalid credentials"}
            )

    return render(request, "registration/login.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect('login_page')



@login_required
def user_profile(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)
    questions = Question.objects.filter(author=profile_user)
    answers = Answer.objects.filter(author=profile_user)

    if request.method == "POST" and request.user == profile_user:
        profile_user.first_name = request.POST.get('first_name')
        profile_user.last_name = request.POST.get('last_name')
        profile_user.bio = request.POST.get('bio')
        profile_user.gender = request.POST.get('gender')
        profile_user.save()
        return redirect('user_profile', username=username)

    return render(request, 'mainapp/user_profile.html', {
        'profile_user': profile_user,
        'questions': questions,
        'answers': answers
    })

@login_required
def dashboard(request):
    # handle form submissions
    if request.method == "POST":
        if 'answer_submit' in request.POST:
            question_id = request.POST.get('question_id')
            content = request.POST.get('content')
            if question_id and content:
                question = get_object_or_404(Question, id=question_id)
                Answer.objects.create(
                    question=question,
                    author=request.user,
                    content=content
                )
                return redirect(f"{reverse('dashboard')}?open={question_id}")

        elif 'comment_submit' in request.POST:
            answer_id = request.POST.get('answer_id')
            question_id = request.POST.get('question_id')
            text = request.POST.get('text')
            if answer_id and text:
                answer = get_object_or_404(Answer, id=answer_id)
                Comment.objects.create(
                    answer=answer,
                    author=request.user,
                    text=text
                )
                return redirect(f"{reverse('dashboard')}?open={question_id}")

    # sort logic
    sort_by = request.GET.get('sort', 'recent')
    questions = Question.objects.annotate(
        total_answers=Count('answers'),
        total_likes=Count('likes')
    ).prefetch_related(
        'answers__author', 'answers__likes', 'answers__comments__author'
    )

    if sort_by == 'answers':
        questions = questions.order_by('-total_answers')
    elif sort_by == 'likes':
        questions = questions.order_by('-total_likes')
    else:
        questions = questions.order_by('-created_at')

    # liked questions/answers
    user_liked_qids = set(
        QuestionLike.objects.filter(user=request.user).values_list('question_id', flat=True)
    )
    user_liked_answer_ids = set(
        AnswerLike.objects.filter(user=request.user).values_list('answer_id', flat=True)
    )

    return render(request, 'mainapp/dashboard.html', {
        'questions': questions,
        'user_liked_qids': user_liked_qids,
        'user_liked_answer_ids': user_liked_answer_ids,
        'active_sort': sort_by,
    })



@login_required
def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answers.annotate(likes_count=Count("likes")).order_by("-created_at")

    user_liked_answer_ids = set(
        AnswerLike.objects.filter(
            user=request.user, answer__question=question
        ).values_list("answer_id", flat=True)
    )

    form = AnswerForm()
    comment_form = CommentForm()

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            answer_id = request.POST.get('answer_id')
            answer = get_object_or_404(Answer, id=answer_id)

            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.answer = answer
                comment.save()
                return redirect('question_detail', pk=question.pk)
            else:
                form = AnswerForm()  # ensure fresh answer form

        else:
            form = AnswerForm(request.POST)
            if form.is_valid():
                answer = form.save(commit=False)
                answer.question = question
                answer.author = request.user
                answer.save()
                return redirect('question_detail', pk=question.pk)
            else:
                comment_form = CommentForm()  # ensure fresh comment form

    return render(
        request,
        "mainapp/question_detail.html",
        {
            "question": question,
            "answers": answers,
            "form": form,
            "comment_form": comment_form,
            "user_liked_answer_ids": user_liked_answer_ids,
            "user_liked_qids": {question.id} if QuestionLike.objects.filter(user=request.user, question=question).exists() else set(),
        },
    )




@login_required
def toggle_question_like(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    like = QuestionLike.objects.filter(question=question, user=request.user).first()

    if like:
        like.delete()
    else:
        QuestionLike.objects.create(question=question, user=request.user)

    return redirect(f"{reverse('dashboard')}?open={question.id}")


@login_required
def edit_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this question.")

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('question_detail', pk=pk)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'mainapp/edit_question.html', {'form': form})

@login_required
def delete_question(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if question.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this question.")

    if request.method == 'POST':
        question.delete()
        return redirect('dashboard')

    return render(request, 'mainapp/confirm_delete.html', {'object': question, 'type': 'question'})

@login_required
def toggle_like(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    like = AnswerLike.objects.filter(answer=answer, user=request.user).first()

    if like:
        like.delete()
    else:
        AnswerLike.objects.create(answer=answer, user=request.user)

    return redirect(f"{reverse('dashboard')}?open={answer.question.id}")


@login_required
def edit_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if answer.author != request.user:
        return HttpResponseForbidden("You are not allowed to edit this answer.")

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            form.save()
            return redirect('question_detail', pk=answer.question.id)
    else:
        form = AnswerForm(instance=answer)

    return render(request, 'mainapp/edit_answer.html', {'form': form, 'answer': answer})


@login_required
def delete_answer(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id)
    if answer.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this answer.")

    if request.method == 'POST':
        question_id = answer.question.id
        answer.delete()
        return redirect('question_detail', pk=question_id)

    return render(request, 'mainapp/confirm_delete.html', {'object': answer, 'type': 'answer'})


@login_required
def post_question(request):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            return redirect("dashboard")
    else:
        form = QuestionForm()

    return render(request, "mainapp/post_question.html", {"form": form})
