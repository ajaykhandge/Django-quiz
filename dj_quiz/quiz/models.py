from django.db import models
from django.contrib.auth.models import User


QUIZES_NAME = (
    ('COC','Clash of Codes'),
    ('WEBER','Weber'),
    ('HOTKEYS','Hotkeys'),
     
    
)


class QuizModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    user_quiz_name = models.CharField(max_length=100,choices=QUIZES_NAME,blank=False,null=False,default='COC')
    user_quiz_attempted = models.BooleanField(blank=False,default=False)
    user_quiz_score = models.IntegerField(default=0,blank=False, null=False)

    def __str__(self):
        return f'{self.user}{self.user_quiz_name}'


'''
COC ==>1-10;
WEBER==>11-20;
HOTKEYS==>21-30;
'''
class QuestionModel(models.Model):
    quest_id = models.IntegerField(primary_key=True,unique=True,blank=False,null=False)
    quest_statement = models.CharField(max_length=200,blank=False, null=False)
    quest_status = models.BooleanField(default=True,null=False)   #to be included in the app/not
    quest_category = models.CharField(max_length=100,default='COC',blank =False,null=False,choices=QUIZES_NAME,help_text='question to selected based on the quiz name')

    def __str__(self):
        return self.quest_statement

class AnswerModel(models.Model):   #questions model only for all quizzes
    question = models.ForeignKey(QuestionModel,on_delete=models.CASCADE)
    option_a = models.CharField(max_length=100,blank=False,null=False)
    option_b = models.CharField(max_length=100,blank=False,null=False)
    option_c = models.CharField(max_length=100,blank=False,null=False)
    option_d = models.CharField(max_length=100,blank=False,null=False)
    quest_ans = models.CharField(max_length=100,blank=False, null=False)
    quest_marks = models.IntegerField(default=1,null=False,blank=False)

    def __str__(self):
        return self.question.quest_statement

class UserAnswerModel(models.Model):
    user  = models.ForeignKey(User,on_delete=models.CASCADE)
    quest_id_user = models.ForeignKey(AnswerModel,on_delete=models.CASCADE)
    user_ans = models.CharField(max_length =100,blank=True, null=True)
    user_correct_ans = models.BooleanField(blank=True,null=True,default=False)
    user_quest_attempted = models.BooleanField(default=False,blank=True,null=True)

    def __str__(self):
        return str(self.quest_id_user.question)

 