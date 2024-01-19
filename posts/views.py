from django.http import (
    HttpResponseBadRequest,
    HttpResponseRedirect,
    HttpResponseForbidden,
    HttpResponse,JsonResponse,
)
from django.shortcuts import render, redirect
from django.urls import reverse

from posts.forms import * 
from posts.models import *  
import os,random, csv
from django.utils import timezone
from datetime import timedelta,datetime



def to_admin(request):
    if request.user.is_staff:
        return redirect("posts:to_admin")
    else:
        return redirect("posts:feeds")



def index(req):
    post_latest = Post.objects.order_by("-createDate")[:6]
    
    context1 = {
        "post_latest": post_latest
    }
    return render(req, "index.html", context=context1)



def feeds(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("users:login")

    posts = Post.objects.all()
    comment_form = CommentForm()
    context = {
        "posts": posts,
        "comment_form": comment_form,
    }
    return render(request, "posts/feeds.html", context)







def feeds2(request):
    user = request.user
    if not user.is_authenticated:
        return redirect("users:login")#### 원래있던 자가 아니면 로그인페이지로
    

    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            print(end_date)
            now_date = timezone.now().date()
            print(now_date)

    else:             
        end_date = timezone.now().date() + timedelta(days=1)
        start_date = end_date - timedelta(days=30)   
        
    # posts = Post2.objects.all().order_by("-created2")[:100]
    # posts = Post2.objects.filter(created2__range=[start_date, end_date]).order_by("-created2")
    posts = Post2.objects.filter(
        created2__range=[
            timezone.make_aware(datetime.combine(start_date, datetime.min.time()), timezone.get_current_timezone()),
            timezone.make_aware(datetime.combine(end_date, datetime.max.time()), timezone.get_current_timezone())
        ]
    ).order_by("-created2")
    bible = TextEntry_b.objects.all().order_by('?')

    bible1 = []    
    lll = bible.count()
    for i in range(posts.count()):
        k = i % lll
        bible1.append(bible[k])
    
    bbb = []  
    for a,b in zip(posts,bible1):
        c = {'posts':a,'bible':b}
        bbb.append(c)         

    comment_form = CommentForm()
    context = {
        "posts": bbb,
        "comment_form": comment_form,       
    }
   

    return render(request, "posts/feeds.html", context)






    # if request.method == 'POST':
    #     form = DateRangeForm(request.POST)
    #     if form.is_valid():
    #         start_date = form.cleaned_data['start_date']
    #         end_date = form.cleaned_data['end_date']
    #         print(start_date)
    #         print(end_date)
    #         posts = Post2.objects.filter(created2__range=[start_date, end_date]).order_by("-created2")

    #         # 이제 시작날짜와 도착날짜를 사용하여 원하는 작업을 수행할 수 있습니다.
    #         return render(request, 'posts/admin1.html', {'posts': posts})
    # else:
    #     # today = timezone.now().date()
    #     # one_month_ago = today - timedelta(days=30)
        
    #     end_date = timezone.now().date()
    #     start_date = end_date - timedelta(days=30)


    #     print(start_date)
    #     print(end_date)

    #     posts = Post2.objects.filter(created2__range=[start_date, end_date]).order_by("-created2")
    #     return render(request, 'posts/admin1.html', {'posts': posts})















# 댓글 작성을 처리할 View
def comment_add(request):
    if request.method == "GET":
        # 이 View에 GET요청이 전달되면, 잘못된 요청임을 브라우저에 알려준다.
        return HttpResponseBadRequest()
    # request.POST로 전달된 데이터를 사용해 CommentForm인스턴스를 생성
    form = CommentForm2(data=request.POST)
    if form.is_valid():
        # commit=False옵션으로 메모리상에 Comment객체 생성
        comment = form.save(commit=False)
        # Comment생성에 필요한 사용자정보를 request에서 가져와 할당
        comment.user = request.user
        # DB에 Comment객체 저장
        comment.save()
        # URL로 "next"값을 전달받았다면 댓글 작성 완료 후 전달받은 값으로 이동한다
        if request.GET.get("next"):
            url_next = request.GET.get("next")
        # "next"값을 전달받지 않았다면 피드페이지의 글 위치로 이동한다
        else:
            url_next = reverse("posts:feeds") + f"#post-{comment.post.id}"
        return HttpResponseRedirect(url_next)

# 댓글 작성을 처리할 View
def comment_addtag(request):
    print(1)
    if request.method == "GET":
        # 이 View에 GET요청이 전달되면, 잘못된 요청임을 브라우저에 알려준다.
        return HttpResponseBadRequest()
    # request.POST로 전달된 데이터를 사용해 CommentForm인스턴스를 생성
    form = CommentForm2(data=request.POST)
    if form.is_valid():
        # commit=False옵션으로 메모리상에 Comment객체 생성
        comment = form.save(commit=False)
        # Comment생성에 필요한 사용자정보를 request에서 가져와 할당
        comment.user = request.user
        # DB에 Comment객체 저장
        comment.save()
        # URL로 "next"값을 전달받았다면 댓글 작성 완료 후 전달받은 값으로 이동한다
        if request.GET.get("next"):
            url_next = request.GET.get("next")
            print(url_next)
        # "next"값을 전달받지 않았다면 피드페이지의 글 위치로 이동한다
        else:
            url_next = reverse("posts:tags")
        return HttpResponseRedirect(url_next)



def comment_delete(request, comment_id):
    if request.method == "POST":
        comment = Comment2.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
            url = reverse("posts:feeds") + f"#post-{comment.post.id}"
            return HttpResponseRedirect(url)
        else:
            return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
    else:
        # 이 View에 오는 GET요청은 잘못되었다고 브라우저에 돌려준다
        return HttpResponseBadRequest()





def comment_delete2(request, comment_id):
    if request.method == "POST":
        comment = Comment2.objects.get(id=comment_id)
        if comment.user == request.user:
            comment.delete()
            url = reverse("posts:feeds") + f"#post-{comment.post.id}"
            return HttpResponseRedirect(url)
        else:
            return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
    else:
        # 이 View에 오는 GET요청은 잘못되었다고 브라우저에 돌려준다
        return HttpResponseBadRequest()





def post_delete(request, post_id):
    if request.method == "POST":
        post = Post2.objects.get(id=post_id) 
        # 여기에서 포스트 아이디를 받아온다. 
        ### post.id = 9 아이디 명을 보니 9번 포스트이다. 프린트 해보니
        # photo = PostImage.objects.get(pk = post.id)
        # 프라임키 id를 9번을 넣어주니 이 포스트의 url을 알 수 있다. 
        # print(photo.photo.url)
        if post.user == request.user: ### 내가 작성한 유저가 맞으면
            # 여기서 삭제해준다. 세팅에서 안되서 여기서는 그냥 때려 넣었다. 
            
            # os.remove("G:/python/20231201 django study first/bb_fgtv1"+photo.photo.url)
            post.delete()
            # 9번 포스트니 그냥 지워주면 그냥 지워진다. 
            url = reverse("posts:feeds") 
            return HttpResponseRedirect(url)
            # 여기서 리 다이렉트 url로 옮겨준다. 
        else:
            return HttpResponseForbidden("이 댓글을 삭제할 권한이 없습니다")
    else:
        # 이 View에 오는 GET요청은 잘못되었다고 브라우저에 돌려준다
        return HttpResponseBadRequest()








def post_add(request):
    if request.method == "POST":
        # request.POST로 온 데이터 ("content")는 PostForm으로 처리
        form = PostForm(request.POST)

        if form.is_valid():
            # Post의 "user"값은 request에서 가져와 자동할당한다
            post = form.save(commit=False)
            post.user = request.user
            post.save()

            # Post를 생성 한 후
            # request.FILES.getlist("images")로 전송된 이미지들을 순회하며 PostImage객체를 생성한다
            for image_file in request.FILES.getlist("images"):
                # request.FILES또는 request.FILES.getlist()로 가져온 파일은
                # Model의 ImageField부분에 곧바로 할당한다
                PostImage.objects.create(
                    post=post,
                    photo=image_file,
                )

            # "tags"에 전달 된 문자열을 분리해 HashTag생성
            tag_string = request.POST.get("tags")
            if tag_string:
                tag_name_list = [tag_name.strip() for tag_name in tag_string.split(",")]
                for tag_name in tag_name_list:
                    tag, _ = HashTag.objects.get_or_create(
                        name=tag_name,
                    )
                    # get_or_create로 생성하거나 가져온 HashTag객체를 Post의 tags에 추가한다
                    post.tags.add(tag)

            # 모든 PostImage와 Post의 생성이 완료되면
            # 피드페이지로 이동하여 생성된 Post의 위치로 스크롤되도록 한다
            url = reverse("posts:feeds") + f"#post-{post.id}"
            return HttpResponseRedirect(url)

    # GET요청일 때는 빈 form을 보여주도록한다
    else:        
        form = PostForm()

    context = {"form": form}
    return render(request, "posts/post_add.html", context)


#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################
#############################################

def post_add2(request):
 
    if request.method == "POST":
        # request.POST로 온 데이터 ("content")는 PostForm으로 처리     
        form = PostForm2(request.POST) 

        if form.is_valid():
            # Post의 "user"값은 request에서 가져와 자동할당한다
            post = form.save(commit=False)
            post.user = request.user
            post.save() 

            # "tags"에 전달 된 문자열을 분리해 HashTag생성
            tag_string = request.POST.get("tags")
            if tag_string:
                tag_name_list = [tag_name.strip() for tag_name in tag_string.split(",")]
                for tag_name in tag_name_list:
                    tag, _ = HashTag.objects.get_or_create(
                        name=tag_name,
                    )
                    # get_or_create로 생성하거나 가져온 HashTag객체를 Post의 tags에 추가한다
                    post.tags.add(tag)

            # 모든 PostImage와 Post의 생성이 완료되면
            # 피드페이지로 이동하여 생성된 Post의 위치로 스크롤되도록 한다
            url = reverse("posts:feeds") + f"#post-{post.id}"   
            return HttpResponseRedirect(url)

    # GET요청일 때는 빈 form을 보여주도록한다
    else:
        form = PostForm2()

    context = {"form": form}
    return render(request, "posts/post_add2.html", context)






def tags(request, tag_name):
    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        # tag_name에 해당하는 HashTag를 찾지 못한 경우 빈 QuerySet을 돌려준다
        posts = Post2.objects.none()
    else:
        posts = Post2.objects.filter(tags=tag)

    # context로 Template에 필터링 된 Post QuerySet을 넘겨주며,
    # 어떤 tag_name으로 검색했는지도 넘겨준다
    context = {
        "tag_name": tag_name,
        "posts": posts,
    }
    return render(request, "posts/tags.html", context)



##################################
##################################
##################################
##################################

def tags2(request, tag_name):

    try:
        tag = HashTag.objects.get(name=tag_name)
    except HashTag.DoesNotExist:
        # tag_name에 해당하는 HashTag를 찾지 못한 경우 빈 QuerySet을 돌려준다
        posts = Post2.objects.none()
    else:
        posts = Post2.objects.filter(tags=tag).all().order_by("-created2")   


    bible = TextEntry_b.objects.all().order_by('?')

    bible1 = []    
    lll = bible.count()
    for i in range(posts.count()):
        k = i % lll
        bible1.append(bible[k])
    
    bbb = []  
    for a,b in zip(posts,bible1):
        c = {'posts':a,'bible':b}
        bbb.append(c)         

    # comment_form = CommentForm()
    # context = {
    #     "posts": bbb,
    #     "comment_form": comment_form,       
    # }  


    comment_form = CommentForm()
    context = {
        "tag_name": tag_name,
        "posts": bbb,
        "comment_form": comment_form,    
    }

    return render(request, "posts/tags.html", context)

 












def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comment_form = CommentForm()
    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, "posts/post_detail.html", context)

def post_detail2(request, post_id):
    print(post_id)
    post = Post2.objects.get(id=post_id)
    comment_form = CommentForm2()
    context = {
        "post": post,
        "comment_form": comment_form,
    }
    return render(request, "posts/post_detail.html", context)


# URL에서 좋아요 처리할 Post의 id를 전달받는다.
def post_like(request, post_id):
    post = Post.objects.get(id=post_id)
    user = request.user

    # 사용자가 "좋아요를 누른 Post목록"에 "좋아요 버튼을 누른 Post"가 존재한다면
    if user.like_posts.filter(id=post.id).exists():
        # 좋아요 목록에서 삭제한다
        user.like_posts.remove(post)

    # 존재하지 않는다면 좋아요 목록에 추가한다.
    else:
        user.like_posts.add(post)

    # next로 값이 전달되었다면 해당 위치로, 전달되지 않았다면 피드페이지에서 해당 Post위치로 이동한다
    url_next = request.GET.get("next") or reverse("posts:feeds") + f"#post-{post.id}"
    return HttpResponseRedirect(url_next)



# URL에서 좋아요 처리할 Post의 id를 전달받는다.
def post_like2(request, post2_id):
    post = Post2.objects.get(id=post2_id)
    user = request.user

    # 사용자가 "좋아요를 누른 Post목록"에 "좋아요 버튼을 누른 Post"가 존재한다면
    if user.like_posts.filter(id=post.id).exists():
        # 좋아요 목록에서 삭제한다
        user.like_posts.remove(post)
        url =  reverse("posts:feeds") + f"#post-{post.id}"
        return HttpResponseRedirect(url)

    # 존재하지 않는다면 좋아요 목록에 추가한다.
    else:
        user.like_posts.add(post)

    # next로 값이 전달되었다면 해당 위치로, 전달되지 않았다면 피드페이지에서 해당 Post위치로 이동한다
    url =  reverse("posts:feeds") + f"#post-{post.id}"
    return HttpResponseRedirect(url)












def text_entry_list(request):
    text_entries = TextEntry_b.objects.all()
    if text_entries:
        random_entry = random.choice(text_entries)
    else:
        random_entry = None

    print(random_entry)

    return render(request, 'posts/post1.html', {'random_entry': random_entry})


   

def admin1(request):
    posts = Post2.objects.all().order_by("-created2")
    return render(request, 'posts/admin1.html', {'posts': posts})






def delete_row(request, row_id):
    try:
        post = Post2.objects.get(pk=row_id)
        post.delete()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'success': False})




def download_csv(request):

    def get_day_name(date):
        days = ['월', '화', '수', '목', '금', '토', '일']
        day_index = date.weekday()
        return days[day_index]      

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_Date')
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="DownLoadCSV.csv"'
    response.write(u'\ufeff'.encode('utf-8'))

    writer = csv.writer(response)
    writer.writerow(['글번호', '아이디', '작성일시','요일',
                      '전화번호', '연령','성별','결혼여부','종교',
                      '직분','신앙상태','정서상태','학력','직업',
                      '내용분류','상담시간',
                      '호소한내용', '솔루션', '느낀점', '상담사례','tag', '팀장확인'])  # 필드 이름을 CSV 파일의 첫 행으로 추가

    # data =Post2.objects.order_by("-created2")[:10000]
    # data = Post2.objects.filter(created2__range=[start_date, end_date]).order_by("-created2")
    data = Post2.objects.filter(
                created2__range=[ timezone.make_aware(datetime.combine(start_date, datetime.min.time()), timezone.get_current_timezone()),
                    timezone.make_aware(datetime.combine(end_date, datetime.max.time()), timezone.get_current_timezone())
                ]).order_by("-created2")
    # data = Post2.objects.filter(created2__range=[start_date, end_date]).order_by("-created2")
    # 여기에 어떤 데이터가 들어가있는지 전부를 봐야한다. DB가 많으면 용량이 너무 커진다
    # 추후에 양을 줄이는 방법도 생각해 볼만하다 일단 초기에는 전부로 한다. 
    # def tags_marriageA(data):
    tags_marriageA = {'0': 'PASS','1': '기혼',  '2': '미혼', '3': '기타'}
    religionA = {'0': 'PASS','1': '본교','2': '타교','3': '불신','4': '기타'}
    tags_condition_AA= { '0': 'PASS','1': '성숙', '2': '미성숙',  '3': '양호',  '4': '기타'}
    tag_condition_BA= { '0': 'PASS', '1': '안정', '2': '불안정', '3': '양호', '4': '기타'}
    
    # b = a.get(1)
        
    for item in data:
        tag2 = ""
        for b in item.tags.all():
            tag2 = tag2 +"| "+ str(b.name) 
        likeuser =""
        for b in item.like_users.all():
            likeuser = likeuser +", #"+ str(b.first_name)+str(b.last_name)
        

        writer.writerow([item.id, item.user, item.created2, get_day_name(item.created2),
                         item.tags_phone,item.tags_years,item.tags_gender,
                         tags_marriageA.get(item.tags_marriage),
                         religionA.get(item.tags_religion),item.tags_position,
                         tags_condition_AA.get(item.tag_condition_A),
                         tag_condition_BA.get(item.tag_condition_B),
                         item.education,item.job,item.a_class_a,item.consult_time,
                         item.content_a,item.content_b,
                         item.content_c,item.content_d,tag2[2:],likeuser[2:] ]) 
        # 여기에서 파라메타 명은 model에 가서 가져온다. 
    return response



def admin2(request):
    posts = TextEntry_b.objects.all()
    return render(request, 'posts/admin2.html', {'posts': posts})


def create_text_entry(request):
    if request.method == 'POST':
        form = TextEntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:admin2')  # 성공 페이지로 리다이렉트
    else:
        form = TextEntryForm()

    return render(request, 'posts/admin2.html', {'form': form})


def delete_row2(request, row_id):
    try:
        post = TextEntry_b.objects.get(pk=row_id)
        post.delete()
        return JsonResponse({'success': True})
    except Post.DoesNotExist:
        return JsonResponse({'success': False})










def date_range_view(request):
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
         
            posts = Post2.objects.filter(
                created2__range=[
                    timezone.make_aware(datetime.combine(start_date, datetime.min.time()), timezone.get_current_timezone()),
                    timezone.make_aware(datetime.combine(end_date, datetime.max.time()), timezone.get_current_timezone())
                ]).order_by("-created2")
            # 이제 시작날짜와 도착날짜를 사용하여 원하는 작업을 수행할 수 있습니다.
            return render(request, 'posts/admin1.html', {'posts': posts})
    else:       
        end_date = timezone.now().date()
        start_date = end_date - timedelta(days=30)


        # posts = Post2.objects.filter(created2__range=[start_date, end_date]).order_by("-created2")
        posts = Post2.objects.filter(
        created2__range=[
            timezone.make_aware(datetime.combine(start_date, datetime.min.time()), timezone.get_current_timezone()),
            timezone.make_aware(datetime.combine(end_date, datetime.max.time()), timezone.get_current_timezone())
        ]).order_by("-created2")
        return render(request, 'posts/admin1.html', {'posts': posts})

