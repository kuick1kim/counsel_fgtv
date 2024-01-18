from django.db import models
from django.core.exceptions import ValidationError
import re

class TextEntry_a(models.Model):
    text_content = models.TextField("공지사항", blank=True)

    def __str__(self):
        return self.text_content
    
class TextEntry_b(models.Model):
    text_content = models.TextField("성경말씀", blank=True)

    def __str__(self):
        return self.text_content



class Post(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    content = models.TextField("내용", blank=True)
    created = models.DateTimeField("작성일시", auto_now_add=True)
    tags = models.ManyToManyField("posts.HashTag", verbose_name="해시태그 목록", blank=True)

    def __str__(self):
        return f"{self.user.username}의 Post(id: {self.id})"
    





class Post2(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    content_a = models.TextField("호소한내용", blank=True)
    content_b = models.TextField("솔루션", blank=True)
    content_c = models.TextField("느낀점", blank=True)
    content_d = models.TextField("상담사례", blank=True)
    created2 = models.DateTimeField("작성일시", auto_now_add=True)
    tags = models.ManyToManyField("posts.HashTag", verbose_name="해시태그 목록", blank=True)   
    
    tags_phone = models.CharField("전화번호",max_length=15, blank=True,help_text='숫자만 넣어주세요 : 0101231234')
    years_CHOICES = [ ('0', '모름'), ('1', '10대'),('2', '20대'),('3', '30대'),('4', '40대'),('5', '50대'),('6', '60대'),('7', '70대') ]
    tags_years = models.CharField("연령",max_length=1, choices=years_CHOICES,blank=True)
    GENDER_CHOICES = [        ('M', '남성'),        ('F', '여성'),  ]
    tags_gender = models.CharField("성별",max_length=1, choices=GENDER_CHOICES,blank=True)
    marriage = [('0', 'PASS'),('1', '기혼'),  ('2', '미혼'), ('3', '기타'),  ]
    tags_marriage = models.CharField("결혼여부",max_length=1, choices=marriage, blank=True)
    religion= [ ('0', 'PASS'),('1', '본교'),('2', '타교'),('3', '불신'),('4', '기타')]
    tags_religion = models.CharField("종교",max_length=1, choices=religion, blank=True,help_text='본교:1 타교:2 불신:3 기타:4')
 
    tags_position = models.CharField("직분",max_length=10, help_text='직분',blank=True)
    condition_A= [ ('0', 'PASS'),('1', '성숙'),('2', '미성숙'),('3', '양호'),('4', '기타')]
    tag_condition_A = models.CharField("신앙상태",max_length=1, choices=condition_A, blank=True,help_text='신앙상태 성숙:1 미성숙:2 양호:3 기타:4')
    condition_B= [ ('0', 'PASS'),('1', '안정'),('2', '불안정'),('3', '양호'),('4', '기타')]
    tag_condition_B = models.CharField("정서상태",max_length=1, choices=condition_B, blank=True,help_text='정서상태 안정:1 불안정:2 중간:3 기타:4')

    education = models.CharField("학력",max_length=10, blank=True,help_text='학력')
    job = models.CharField("직업",max_length=10, blank=True,help_text='직업')
    a_class_a = models.CharField("내용분류",max_length=10, blank=True,help_text='내용분류')
    consult_time = models.CharField("상담시간",max_length=3, blank=True,help_text='ex: 20분:20')
    

    def clean_phone_number(self):
        # 정규 표현식을 사용하여 숫자만 허용하는 유효성 검사        
        phone_number = self.phone_number
        if not re.match(r'^\+?\d+$', phone_number):
            raise ValidationError('Phone number can only contain digits.')

    def __str__(self):
        return f"{self.user.username}의 Post2(id: {self.id})"






class PostImage(models.Model):
    post = models.ForeignKey(Post, verbose_name="포스트", on_delete=models.CASCADE)
    photo = models.ImageField("사진", upload_to="post")


class Comment(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    post = models.ForeignKey(Post, verbose_name="포스트", on_delete=models.CASCADE)
    content = models.TextField("내용")
    created = models.DateTimeField("작성일시", auto_now_add=True)



class Comment2(models.Model):
    user = models.ForeignKey("users.User", verbose_name="작성자", on_delete=models.CASCADE)
    post = models.ForeignKey(Post2, verbose_name="포스트", on_delete=models.CASCADE)
    content = models.TextField("내용")
    created = models.DateTimeField("작성일시", auto_now_add=True)


class HashTag(models.Model):
    name = models.CharField("태그명", max_length=50)

    def __str__(self):
        return self.name
