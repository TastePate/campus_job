from rest_framework import serializers
from .models import Job, Application, Resume

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('resume', 'cover_letter')
        extra_kwargs = {
            'cover_letter': {'required': False, 'allow_blank': True}
        }

    def validate_resume(self, value):
        if value.user != self.context['request'].user:
            raise serializers.ValidationError("Вы можете использовать только своё резюме.")
        return value

    def validate(self, data):
        if not self.context['request'].user.is_authenticated:
            raise serializers.ValidationError("Требуется аутентификация.")
        return data

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        job_pk = self.context['view'].kwargs.get('pk')
        try:
            job = Job.objects.get(pk=job_pk)
        except Job.DoesNotExist:
            raise serializers.ValidationError({"job": "Вакансия не существует."})
        validated_data['job'] = job
        return super().create(validated_data)
