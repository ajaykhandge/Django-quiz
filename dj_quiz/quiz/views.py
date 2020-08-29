from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import QuestionModel,AnswerModel,UserAnswerModel,QuizModel
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import User
from django.db.models import Count,Case,When,Value
 
from django.core import serializers
from django.contrib.auth import authenticate,logout

# Create your views here.
QUIZES_NAME = (
    ('COC','Clash of Codes'),
    ('WEBER','Weber'),
    ('HOTKEYS','Hotkeys'),
     
    
)

#view for welcome to quiz
def index(request):
    context = {

    }
    return render(request,'quiz/index.html',context)

#view for explaining rules and regs.
@login_required
def welcome(request):
    if request.user.is_superuser:
        return redirect('/leaderboard')  
        #current user is admin
    else: 
        #gets the current user and fetch its info
        print(int(request.user.participant.phone_no))
        #checking if the user attempted quiz or not
        try:
            current_user_quiz = QuizModel.objects.filter(user=request.user).exists()

            if(current_user_quiz):
                user_quiz_model_instance = QuizModel.objects.get(user=request.user)
                if user_quiz_model_instance.user_quiz_attempted:

                    return redirect('forbidden')
            if not current_user_quiz:
                current_user_quiz = QuizModel(user=request.user,user_quiz_name=request.user.participant.quiz_name)
                current_user_quiz.save(force_insert=True)
        except:
            pass
                
    
    return render(request,'quiz/welcome.html')

def check_question(request):
    
    if request.is_ajax and request.method == 'POST':
        #get the stuff
        current_quest_id = int(request.POST.get('current_question_id'))
        option_selected = request.POST.get('selected_option')
        

        current_quest_instance  = QuestionModel.objects.get(pk=current_quest_id)
        current_ans_instance  = AnswerModel.objects.get(question = current_quest_instance)

        quest_ans_status = False

        if current_ans_instance.quest_ans == option_selected.lower():
            quest_ans_status = True
        
   

        #if the user has already attempte the question then the old object will updated instead of creating new one.

        if UserAnswerModel.objects.filter(user=request.user,quest_id_user=current_ans_instance).exists():
            inst = UserAnswerModel.objects.get(user=request.user,quest_id_user=current_ans_instance)
            user_ans_model_instance = UserAnswerModel(user=request.user,quest_id_user=current_ans_instance,user_ans=option_selected.lower(),user_correct_ans=quest_ans_status,user_quest_attempted=True)
            user_ans_model_instance.id = inst.id
            user_ans_model_instance.save(force_update=True)
            quiz_model_instance = QuizModel.objects.get(user=request.user)

            if(quest_ans_status):
                quiz_model_instance.user_quiz_score+=current_ans_instance.quest_marks
            else:
                quiz_model_instance.user_quiz_score-=current_ans_instance.quest_marks
            quiz_model_instance.save()

            #updates the score of user
             
        else:
            #gets its marks
            if(quest_ans_status):
                quiz_model_instance = QuizModel.objects.get(user=request.user)
                quiz_model_instance.user_quiz_score+=current_ans_instance.quest_marks
                quiz_model_instance.save()

            user_ans_model_instance = UserAnswerModel(user=request.user,quest_id_user=current_ans_instance,user_ans=option_selected.lower(),user_correct_ans=quest_ans_status,user_quest_attempted=True)
            user_ans_model_instance.save(force_insert=True)


        #load the next question or current based on its position.
        
        if current_quest_id != QuestionModel.objects.count():
            next_quest_instance = QuestionModel.objects.get(pk=current_quest_id+1)
            next_ans_instance = AnswerModel.objects.get(question=next_quest_instance)
            try:
                bool_user_ans =   UserAnswerModel.objects.filter(user=request.user,quest_id_user=next_ans_instance).exists()
                user_ans_instance = UserAnswerModel.objects.get(user=request.user,quest_id_user=next_ans_instance)
                user_ans_status = {
                    'attempted':user_ans_instance.user_quest_attempted,
                    'option_selected':user_ans_instance.user_ans
                }
            except:
                user_ans_status = {
                    'attempted':'False',
                    'option_selected':'a'
                }



            ser_next_quest_instance = serializers.serialize('json',[next_quest_instance])
            ser_next_ans_instance = serializers.serialize('json',[next_ans_instance])

            
        else:
            try:
                bool_user_ans =   UserAnswerModel.objects.filter(user=request.user,quest_id_user=current_ans_instance).exists()
                user_ans_instance = UserAnswerModel.objects.get(user=request.user,quest_id_user=current_ans_instance)
                user_ans_status = {
                    'attempted':user_ans_instance.user_quest_attempted,
                    'option_selected':user_ans_instance.user_ans
                }
            except:

                user_ans_status = {
                    'attempted':'False',
                    'option_selected':'a'
                }
            ser_next_quest_instance = serializers.serialize('json',[current_quest_instance,])
            ser_next_ans_instance = serializers.serialize('json',[current_ans_instance])

             
        
        return JsonResponse({'quest_instance':ser_next_quest_instance,'ans_instance':ser_next_ans_instance,'user_ans':user_ans_status})
    
  
         
 

#a view that will acts as JSON view
@login_required(login_url='/login')
def quiz_question(request):

    if request.is_ajax and request.method =='POST':
        quest_id = int(request.POST.get('quest_id'))
        print(quest_id)

        instance = QuestionModel.objects.get(pk=quest_id,quest_status=True,quest_category=request.user.participant.quiz_name)
        print(instance)
        option_model = AnswerModel.objects.get(question = instance)
        print(option_model.question)

        #answer model 
        try:
            bool_user_ans =   UserAnswerModel.objects.filter(user=request.user,quest_id_user=option_model).exists()
            user_ans_instance = UserAnswerModel.objects.get(user=request.user,quest_id_user=option_model)
            user_ans_status = {
                'attempted':user_ans_instance.user_quest_attempted,
                'option_selected':user_ans_instance.user_ans
            }
        except:
            user_ans_status = {
                'attempted':'False',
                'option_selected':'a'
            }

            

        ser_instance = serializers.serialize('json',[option_model,])
        option_question = serializers.serialize('json',[instance])


         
        return JsonResponse({'instance':ser_instance,'question':option_question,'user_ans':user_ans_status})

         
def quiz_test(request):
    try:

        current_user_quiz = QuizModel.objects.filter(user=request.user).exists()
        if(current_user_quiz):
            user_quiz_model_instance = QuizModel.objects.get(user=request.user)
            if user_quiz_model_instance.user_quiz_attempted:
                print('False')
                return False
            else:
                print('True')
                return True
        else:
            return True
           
            
    except:
        pass


@login_required(redirect_field_name='welcome')
def quiz(request):

    #currently user is login and marking its quiz attempt as False
  
    return render(request,'quiz/quiz.html')


   
        
    


def thanks(request):
    user = request.user
    
    #making the current user logined logout and quiz_attempted_status=Truu
    quiz_user = QuizModel.objects.get(user=request.user)
    quiz_user.user_quiz_attempted = True
    quiz_user.save(force_update=True)
  

    logout(request)
     
    print(request.user)


    context={
        'message':f'Congratulations!!!{user }. You have successfully attempted the QUIZ Round'
         
    
    }
    return render(request,'quiz/thanks.html',context)



@user_passes_test(lambda u: u.is_superuser)
def leaderboard(request):

    list_users = []

    #calculating the scores of user
    quiz_users = User.objects.exclude(is_superuser=True)
    print(quiz_users)
    '''
    for user in quiz_users:
        ans_user = UserAnswerModel.objects.filter(user=user)

        count_val=ans_user.aggregate(
        bool_col=Count(
        Case(When(user_correct_ans=True, then=Value(2)))
         ))
        print(count_val.get('bool_col'))

        list_users.append({
             'name':user.username,
             'email':user.email,
             'college_name':user.participant.college_name,
             'score':count_val.get('bool_col')
         })
        '''
    #getting the score to leaderboard
    all_quiz_users = QuizModel.objects.all().order_by('-user_quiz_score')



    context ={
             'list':all_quiz_users
         }
    
    print(list_users)

          
         
         

       
        

       
     

    

    return render(request,'quiz/leaderboard.html',context)



def forbidden(request):
    context = {
        'mesg':'WE cant allow you to have another chance..!'
    }
    return render(request,'quiz/forbidden.html',context)


