from django.contrib.auth.models import User, Group
from rest_framework import serializers
from quizzes.models import Quizzes
from questions.models import Questions
from answers.models import Answers


class QuizSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Quizzes
        fields = ['id', 'title', 'description', 'user']


class AnswersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answers
        fields = ['id', 'is_correct', 'answer', 'question']
        read_only_fields = ['question']


class QuestionSerializer(serializers.ModelSerializer):
    question_answers = AnswersSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Questions
        fields = ['id', 'question', 'quiz', 'question_answers']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        context = kwargs.get('context', None)
        if context:
            request = kwargs['context']['request']
            if request.method in ['POST']:
                self.fields['question_answers'].required = True

    def create(self, validated_data):
        answers = validated_data.pop('question_answers')
        question = Questions.objects.create(**validated_data)
        for ans in answers:
            # any ingredient logic here
            Answers.objects.create(question=question, **ans)
        return question

    def update(self, instance, validated_data):
        validated_data.pop('question_answers')
        instance.question = validated_data['question']
        instance.save()
        return instance

    def validate_question_answers(self, values):
        print(values)
        if len(values) != 4:
            raise serializers.ValidationError("Please add four options of this question")

        correct_ans = []
        for ans in values:
            if ans['is_correct'] is True:
                correct_ans.append(ans)
        if len(correct_ans) > 1:
            raise serializers.ValidationError("Only one option can be True.")
        if len(correct_ans) < 1:
            raise serializers.ValidationError("One option must be True.")
        return values


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']