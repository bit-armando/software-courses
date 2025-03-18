from django.forms import ModelForm
from .models import Course, Comment, Response
from software_courses.storage_backends import MediaStorage


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'image', 'short_description', 'description', 'video']

    def save(self, commit=True):
        instance = super().save(commit=False)
        media_storage = MediaStorage()

        # Save video to S3
        video = self.cleaned_data.get('video')
        if video:
            video_name = media_storage.save(f"videos/{video.name}", video)
            instance.video = media_storage.url(video_name)

        # Save image to S3
        image = self.cleaned_data.get('image')
        if image:
            image_name = media_storage.save(f"courses_img/{image.name}", image)
            instance.image = media_storage.url(image_name)

        if commit:
            instance.save()
        return instance

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'

class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = '__all__'