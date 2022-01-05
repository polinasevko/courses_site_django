from rest_framework import serializers
from .models import Course, Lecture, Hometask, Homework, Mark


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.StringRelatedField(many=True)
    students = serializers.StringRelatedField(many=True)

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['teachers'].append(user.id)
        instance = super().create(validated_data)
        return instance

    # prevent teachers/students fields from being updated
    def update(self, instance, validated_data):
        validated_data.pop('teachers', None)
        validated_data.pop('students', None)
        return super().update(instance, validated_data)


class AddTeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('teachers',)

    def validate(self, attrs):
        teachers = attrs.get('teachers', self.instance.teachers.all())
        students = attrs.get('students', self.instance.students.all())
        if set(teachers).intersection(students):
            raise serializers.ValidationError({"teachers": "The same user cannot be both teacher and student."})
        return attrs

    def update(self, instance, validated_data):
        for teacher in validated_data['teachers']:
            instance.teachers.add(teacher.id)
        return instance


class AddDeleteStudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('students',)

    def validate(self, attrs):
        teachers = attrs.get('teachers', self.instance.teachers.all())
        students = attrs.get('students', self.instance.students.all())
        if set(teachers).intersection(students):
            raise serializers.ValidationError({"students": "The same user cannot be both teacher and student."})
        return attrs

    def update(self, instance, validated_data):
        for student in validated_data['students']:
            instance.students.add(student.id)
        return instance


class LectureSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()

    class Meta:
        model = Lecture
        fields = '__all__'

    def create(self, validated_data):
        course_id = self.context['view'].kwargs['course_pk']
        validated_data['course'] = Course.objects.get(id=course_id)
        instance = super().create(validated_data)
        return instance

    # prevent course field from being updated
    def update(self, instance, validated_data):
        validated_data.pop('course', None)
        return super().update(instance, validated_data)


class HometaskSerializer(serializers.ModelSerializer):
    lecture = serializers.StringRelatedField()

    class Meta:
        model = Hometask
        fields = '__all__'

    def create(self, validated_data):
        lecture_id = self.context['view'].kwargs['lecture_pk']
        validated_data['lecture'] = Hometask.objects.get(id=lecture_id)
        instance = super().create(validated_data)
        return instance

    # prevent lecture field from being updated
    def update(self, instance, validated_data):
        validated_data.pop('lecture', None)
        return super().update(instance, validated_data)


class HomeworkSerializer(serializers.ModelSerializer):
    # student = serializers.HiddenField(default=serializers.CurrentUserDefault())
    hometask = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = Homework
        fields = '__all__'

    def create(self, validated_data):
        hometask_id = self.context['view'].kwargs['hometask_pk']
        validated_data['hometask'] = Hometask.objects.get(id=hometask_id)
        validated_data['student'] = self.context['request'].user
        instance = super().create(validated_data)
        return instance

    # prevent student/hometask field from being updated
    def update(self, instance, validated_data):
        validated_data.pop('hometask', None)
        validated_data.pop('student', None)
        return super().update(instance, validated_data)


class MarkSerializer(serializers.ModelSerializer):
    homework = serializers.StringRelatedField()

    class Meta:
        model = Mark
        fields = '__all__'

    def create(self, validated_data):
        homework_id = self.context['view'].kwargs['homework_pk']
        validated_data['homework'] = Homework.objects.get(id=homework_id)
        instance = super().create(validated_data)
        return instance

    # prevent homework field from being updated
    def update(self, instance, validated_data):
        validated_data.pop('homework', None)
        return super().update(instance, validated_data)
