import datetime

from django.utils import timezone

from .models import Wares, Waregroups, Events, Waresingroup, Pricesinevent


#class waresMethodTests(TestCase):
    
    #def test_insertware(self):
        #Tests that a ware can be inserted with insert function
        #insertware("Carslberg")

"""
class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
                was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_recent_question(self):
        
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        
        time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)
        
class HelperfunctionsMethodTest(TestCase):
    
    helpfunct = Helperfunctions()
    
    def test_insertware(self):
        #Tests that a ware can be inserted with insert function
        helpfunct.insertware("Carslberg")
        helpfunct.setwareinbar(1, 5)
        self.assertEqual(len(Wares.objects.all().filter(inbar=5)) == 1, True)
"""
