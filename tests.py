import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_default_values():
    question = Question(title='Sample Question')
    assert question.points == 1
    assert question.max_selections == 1

def test_create_question_with_custom_values():
    question = Question(title='Sample Question', points=10, max_selections=3)
    assert question.points == 10
    assert question.max_selections == 3

def test_add_choice_with_max_length_text():
    question = Question(title='Sample Question')
    text = 'A' * 100
    choice = question.add_choice(text)
    assert choice.text == text

def test_add_choice_with_special_characters():
    question = Question(title='Sample Question')
    choice = question.add_choice('Opção @#!$')
    assert choice.text == 'Opção @#!$'

def test_remove_choice_and_validate_ids():
    question = Question(title='Sample Question')
    choice1 = question.add_choice('Choice A')
    choice2 = question.add_choice('Choice B')
    
    question.remove_choice_by_id(choice1.id)
    assert choice1.id not in [c.id for c in question.choices]

def test_set_all_choices_correct():
    question = Question(title='Sample Question')
    choice1 = question.add_choice('Choice A')
    choice2 = question.add_choice('Choice B')
    question.set_correct_choices([choice1.id, choice2.id])
    
    assert all(choice.is_correct for choice in question.choices)

def test_set_no_correct_choices():
    question = Question(title='Sample Question')
    choice1 = question.add_choice('Choice A', is_correct=True)
    choice2 = question.add_choice('Choice B', is_correct=True)

    question.set_correct_choices([])

    assert set(question._correct_choice_ids()) == {choice1.id, choice2.id}

def test_select_only_correct_choices():
    question = Question(title='Sample Question', max_selections=3) 
    choice1 = question.add_choice('Choice A', is_correct=True)
    choice2 = question.add_choice('Choice B', is_correct=False)
    choice3 = question.add_choice('Choice C', is_correct=True)
    
    selected = question.select_choices([choice1.id, choice2.id, choice3.id])
    assert selected == [choice1.id, choice3.id]

def test_add_choice_and_validate_ids():
    question = Question(title='Sample Question')
    choice1 = question.add_choice('Choice A')
    choice2 = question.add_choice('Choice B')
    
    assert choice1.id != choice2.id

def test_create_question_with_edge_case_points():
    with pytest.raises(Exception):
        Question(title='Sample Question', points=0)
    with pytest.raises(Exception):
        Question(title='Sample Question', points=101)

@pytest.fixture
def sample_question():
    question = Question(title='Sample Question', max_selections=3)
    choice1 = question.add_choice('Choice A', is_correct=True)
    choice2 = question.add_choice('Choice B', is_correct=False)
    choice3 = question.add_choice('Choice C', is_correct=True)
    return question

@pytest.fixture
def question_with_limited_selections():
    question = Question(title='Limited Selections Question', max_selections=2)
    question.add_choice('Choice A', is_correct=True)
    question.add_choice('Choice B', is_correct=False)
    question.add_choice('Choice C', is_correct=True)
    return question

def test_select_correct_choices(sample_question):
    selected = sample_question.select_choices([c.id for c in sample_question.choices])
    assert set(selected) == set(sample_question._correct_choice_ids())

def test_remove_all_choices(sample_question):
    sample_question.remove_all_choices()
    assert len(sample_question.choices) == 0

def test_max_selection_limit(question_with_limited_selections):
    choices = [choice.id for choice in question_with_limited_selections.choices]
    with pytest.raises(Exception, match="Cannot select more than 2 choices"):
        question_with_limited_selections.select_choices(choices)