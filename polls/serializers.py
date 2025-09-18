from rest_framework import serializers
from .models import Question, Choice, Answer


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        read_only_fields = ["id"]
        fields = ["id",
                  "choice_text",
                  "order"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        read_only_fields = ['id']
        fields = ["id","choice"]

# class QuestionSerializer(serializers.ModelSerializer):
#     choices = ChoiceSerializer(many=True)
#     answers = serializers.SerializerMethodField()
#
#     def get_answers(self,obj):
#         user = self.context['request'].user
#         answers = obj.answers.filter(user=user)
#         serializer = AnswerSerializer(answers,many=True)
#         return serializer.data
#
#
#     class Meta:
#         model = Question
#         read_only_fields = ["id"]
#         fields = [
#             "id",
#             "question_text",
#             "pub_date",
#             "choices",
#             "answers",
#         ]




    def create(self, validated_data):
        choices = validated_data.pop("choices")
        question = super().create(validated_data)
        Choice.objects.bulk_create([Choice(**choice,question=question) for choice in choices])
        return question


class QuestionPreviewSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        read_only_fields = ['id']
        fields = [
            "id",
            "question_text",
            "pub_date",
            "choices"]

class QuestionSerializer(QuestionPreviewSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = QuestionPreviewSerializer.Meta.fields + ["answers"]

    def get_answers(self, obj):
        user = self.context['request'].user
        answers = obj.answers.filter(user=user)
        serializer = AnswerSerializer(answers,many=True)
        return serializer.data