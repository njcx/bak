def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})

####好习惯，404页面
from django.shortcuts import get_object_or_404, render

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

####快捷404页面


>>> from polls.models import Question, Choice   # Import the model classes we just wrote.
>>> Question.objects.all()
[]
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())
>>> q.save()
>>> q.id
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=<UTC>)
>>> q.question_text = "What's up?"
>>> q.save()
>>> Question.objects.all()
[<Question: Question object>]

#### orm APi

>>> from polls.models import Question, Choice

>>> Question.objects.all()
[<Question: What's up?>]
>>> Question.objects.filter(id=1)
[<Question: What's up?>]
>>> Question.objects.filter(question_text__startswith='What')
[<Question: What's up?>]

>>> from django.utils import timezone
>>> current_year = timezone.now().year
>>> Question.objects.get(pub_date__year=current_year)
<Question: What's up?>
>>> Question.objects.get(id=2)
Traceback (most recent call last):
    ...
DoesNotExist: Question matching query does not exist.
>>> Question.objects.get(pk=1)
<Question: What's up?>
>>> q = Question.objects.get(pk=1)
>>> q.was_published_recently()
True
>>> q = Question.objects.get(pk=1)
>>> q.choice_set.all()
[]
>>> q.choice_set.create(choice_text='Not much', votes=0)
<Choice: Not much>
>>> q.choice_set.create(choice_text='The sky', votes=0)
<Choice: The sky>
>>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)
>>> c.question
<Question: What's up?>
>>> q.choice_set.all()
[<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]
>>> q.choice_set.count()
>>> Choice.objects.filter(question__pub_date__year=current_year)
[<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]
>>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
>>> c.delete()

>>> fruit = Fruit.objects.create(name='Apple')
>>> fruit.name = 'Pear'
>>> fruit.save()
>>> Fruit.objects.values_list('name', flat=True)
['Apple', 'Pear']

#### orm 外键 APi


<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>

#### 正向 与 反向

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^polls/', include('polls.urls', namespace="polls")),
    url(r'^admin/', include(admin.site.urls)),
]

<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>

#### 带有名字空间的url

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from .models import Choice, Question
# ...
def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
//重要        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

#### 标准视图

from django.db import models

class Person(models.Model):
    SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
    name = models.CharField(max_length=60)
    shirt_size = models.CharField(max_length=1, choices=SHIRT_SIZES)

// 自增字段id = models.AutoField(primary_key=True)
####数据库可选文本


字段的自述名¶
除ForeignKey、ManyToManyField 和 OneToOneField 之外，每个字段类型都接受一个可选的位置参数（在第一的位置） —— 字段的自述名。如果没有给定自述名，Django 将根据字段的属性名称自动创建自述名 —— 将属性名称的下划线替换成空格。

在这个例子中，自述名是 "person's first name"：

first_name = models.CharField("person's first name", max_length=30)
在这个例子中，自述名是  "first name"：

first_name = models.CharField(max_length=30)
ForeignKey、ManyToManyField 和 OneToOneField 都要求第一个参数是一个模型类，所以要使用 verbose_name 关键字参数才能指定自述名：

poll = models.ForeignKey(Poll, verbose_name="the related poll")
sites = models.ManyToManyField(Site, verbose_name="list of sites")
place = models.OneToOneField(Place, verbose_name="related place")
习惯上，verbose_name 的首字母不用大写。Django 在必要的时候会自动大写首字母。

####

from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)

####
from blog.models import Entry
entry = Entry.objects.get(pk=1)
cheese_blog = Blog.objects.get(name="Cheddar Talk")
entry.blog = cheese_blog
entry.save()

####外键
>>> john = Author.objects.create(name="John")
>>> paul = Author.objects.create(name="Paul")
>>> george = Author.objects.create(name="George")
>>> ringo = Author.objects.create(name="Ringo")
>>> entry.authors.add(john, paul, george, ringo)

#### 多对多
使用过滤器获取特定对象¶
all() 方法返回了一个包含数据库表中所有记录查询集。但在通常情况下，你往往想要获取的是完整数据集的一个子集。
要创建这样一个子集，你需要在原始的的查询集上增加一些过滤条件。两个最普遍的途径是：
filter(**kwargs)
返回一个新的查询集，它包含满足查询参数的对象。
exclude(**kwargs)
返回一个新的查询集，它包含不满足查询参数的对象。
查询参数（上面函数定义中的**kwargs）需要满足特定的格式，下面字段查询一节中会提到。
举个例子，要获取年份为2006的所有文章的查询集，可以使用filter()方法：
Entry.objects.filter(pub_date__year=2006)
利用默认的管理器，它相当于：
Entry.objects.all().filter(pub_date__year=2006)
查询集的筛选结果本身还是查询集，所以可以将筛选语句链接在一起。像这样：
>>> Entry.objects.filter(
...     headline__startswith='What'
... ).exclude(
...     pub_date__gte=datetime.date.today()
... ).filter(
...     pub_date__gte=datetime(2005, 1, 30)
... )
####查询
字段+ __ (动词）
exact  精确
iexact  忽略大小精确

Entry.objects.get(id__exact=14)
Entry.objects.get(id__exact=None)

SELECT ... WHERE id = 14;
SELECT ... WHERE id IS NULL;

contains  区分大小写的包含例子
icontains  区分大小写的包含例子

Entry.objects.get(headline__contains='Lennon')

Entry.objects.filter(id__gt=4)

gte >=

lt < 

lte <=

in 给定的列表

startswith 区分大小写，开始位置匹配
Entry.objects.filter(headline__startswith='Will')

istartswith 不区分大小写

Entry.objects.filter(headline__istartswith='will')

endswith

iendswith

range 范围测试（包含于之中）。

import datetime
start_date = datetime.date(2005, 1, 1)
end_date = datetime.date(2005, 3, 31)
Entry.objects.filter(pub_date__range=(start_date, end_date))

year
month
day
week_day
hour
minute
second

Entry.objects.filter(pub_date__year=2005)
Entry.objects.filter(pub_date__month=12)
Entry.objects.filter(pub_date__day=3)
Event.objects.filter(timestamp__hour=23)


isnull 是否为空
search 类似全文搜索

// 正则// 
Entry.objects.get(title__regex=r'^(An?|The) +')

iregex // 不区分大小写的正则
