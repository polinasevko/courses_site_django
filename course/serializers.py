from rest_framework import serializers

from .models import Comment, Course, Hometask, Homework, Lecture


class CourseSerializer(serializers.ModelSerializer):
    teachers = serializers.StringRelatedField(many=True, required=False)
    students = serializers.StringRelatedField(many=True, required=False)

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
        validated_data['lecture'] = Lecture.objects.get(id=lecture_id)
        instance = super().create(validated_data)
        return instance

    # prevent lecture field from being updated
    def update(self, instance, validated_data):
        validated_data.pop('lecture', None)
        return super().update(instance, validated_data)


class HomeworkSerializer(serializers.ModelSerializer):
    hometask = serializers.StringRelatedField()
    student = serializers.StringRelatedField()

    class Meta:
        model = Homework
        fields = '__all__'
        read_only_fields = ['mark']

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

    class Meta:
        model = Homework
        fields = ('mark',)

    def validate(self, attrs):
        if attrs['mark'] > self.instance.hometask.max_mark:
            raise serializers.ValidationError({"mark": "Mark cannot be more than Maximum mark for task."})
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    homework = serializers.StringRelatedField()
    owner = serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        homework_id = self.context['view'].kwargs['homework_pk']
        homework_obj = Homework.objects.get(id=homework_id)
        if not homework_obj.mark:
            raise Exception("Mark is null. You can leave comments only on the mark.")

        validated_data['owner'] = user
        validated_data['homework'] = homework_obj
        instance = super().create(validated_data)
        return instance

    # prevent homework/owner field from being updated
    def update(self, instance, validated_data):
        validated_data.pop('homework', None)
        validated_data.pop('owner', None)
        return super().update(instance, validated_data)

