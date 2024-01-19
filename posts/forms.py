from django import forms

from posts.models import *#Comment, Post, Post2


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "post",
            "content",
        ]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "placeholder": "댓글 달기...",
                }
            )
        }


class CommentForm2(forms.ModelForm):
    class Meta:
        model = Comment2
        fields = [
            "post",
            "content",
        ]
        widgets = {
            "content_a": forms.Textarea(
                attrs={
                    "placeholder": "댓글 달기1...",
                }
            ),
            "content_b": forms.Textarea(
                attrs={
                    "placeholder": "댓글 달기2...",
                }
            ),
            "content_c": forms.Textarea(
                attrs={
                    "placeholder": "댓글 달기3...",
                }
            )
        }






class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "content",
        ]



class TextEntryForm_note(forms.ModelForm):
    class Meta:
        model = TextEntry_a
        fields = ['text_content']

class TextEntryForm(forms.ModelForm):
    class Meta:
        model = TextEntry_b
        fields = ['text_content']
       





class PostForm2(forms.ModelForm):
    class Meta:
        model = Post2
        fields = [
            "tags_phone",
            "tags_years",
            "tags_gender",
            "tags_marriage",
            "tags_religion",
            "tag_condition_A",
            "tag_condition_B",
            "education",
            "job",
            "consult_time",
            "content_a",
            "content_b",
            "content_c",
            "content_d",
        ]



class DateRangeForm(forms.Form):
    start_date = forms.DateField(label=('Start Date'))
    end_date = forms.DateField(label=('End Date'))
    # widget=forms.DateInput(attrs={'class': 'datepicker', 'style': 'font-size: 20px;'})

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        # 날짜 유효성 검사
        if start_date and end_date and start_date > end_date:
            raise ValidationError(('Start date should be before end date.'))

        return cleaned_data




