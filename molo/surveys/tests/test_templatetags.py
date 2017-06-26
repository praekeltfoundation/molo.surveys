from django.test import TestCase, RequestFactory
from django.template import Template, Context
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

from molo.core.models import Main, Languages, SiteLanguageRelation
from molo.core.tests.base import MoloTestCaseMixin
from molo.surveys.models import (MoloSurveyPage, MoloSurveyFormField,
                                 SurveysIndexPage)

from molo.surveys.templatetags.molo_survey_tags import get_survey_list


def add_session_to_request(request):
    """Annotate a request object with a session"""
    middleware = SessionMiddleware()
    middleware.process_request(request)
    request.session.save()


class SurveyListTest(TestCase, MoloTestCaseMixin):

    def create_molo_survey_page(self,
                                parent,
                                title="Test Survey",
                                slug="test-survey",
                                **kwargs):
        molo_survey_page = MoloSurveyPage(
            title=title,
            slug=slug,
            intro='Introduction to Test Survey ...',
            thank_you_text='Thank you for taking the Test Survey',
            **kwargs
        )

        parent.add_child(instance=molo_survey_page)
        molo_survey_form_field = MoloSurveyFormField.objects.create(
            page=molo_survey_page,
            sort_order=1,
            label='Your favourite animal',
            field_type='singleline',
            required=True
        )
        return molo_survey_page, molo_survey_form_field

    def setUp(self):
        self.mk_main()
        self.main = Main.objects.all().first()
        self.language_setting = Languages.objects.create(
            site_id=self.main.get_site().pk)
        self.english = SiteLanguageRelation.objects.create(
            language_setting=self.language_setting,
            locale='en',
            is_active=True)
        self.surveys_index = SurveysIndexPage.objects.child_of(
            self.main).first()

        self.user = User.objects.create_user(
            'test', 'test@example.org', 'test')

        # create a requset object
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.site = self.site
        self.request.user = self.user
        add_session_to_request(self.request)

        # create direct questions
        self.direct_molo_survey_page, direct_molo_survey_form_field = \
            self.create_molo_survey_page(
                parent=self.surveys_index,
                title="direct survey title",
                slug="direct_survey_title",
                display_survey_directly=True,
            )

        self.linked_molo_survey_page, linked_molo_survey_form_field = \
            self.create_molo_survey_page(
                parent=self.surveys_index,
                title="linked survey title",
                slug="linked_survey_title",
                display_survey_directly=False,
            )


    def test_get_survey_list_default(self):
        context = Context({
            'locale_code': 'en',
            'request': self.request,
        })
        context = get_survey_list(context)
        self.assertTrue(len(context['surveys'])==2)
        self.assertTrue(self.direct_molo_survey_page in context['surveys'])
        self.assertTrue(self.linked_molo_survey_page in context['surveys'])

    def test_get_survey_list_only_direct(self):
        context = Context({
            'locale_code': 'en',
            'request': self.request,
        })
        context = get_survey_list(context, only_direct_surveys=True)
        self.assertTrue(len(context['surveys'])==1)
        self.assertTrue(self.direct_molo_survey_page in context['surveys'])
        self.assertTrue(self.linked_molo_survey_page not in context['surveys'])

    def test_get_survey_list_only_linked(self):
        context = Context({
            'locale_code': 'en',
            'request': self.request,
        })
        context = get_survey_list(context, only_linked_surveys=True)
        self.assertTrue(len(context['surveys'])==1)
        self.assertTrue(self.direct_molo_survey_page not in context['surveys'])
        self.assertTrue(self.linked_molo_survey_page in context['surveys'])

    def test_get_survey_list_arg_error(self):
        context = Context({
            'locale_code': 'en',
            'request': self.request,
        })
        with self.assertRaises(ValueError):
            context = get_survey_list(context,
                                      only_linked_surveys=True,
                                      only_direct_surveys=True,)
