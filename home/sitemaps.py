from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from userprofile.models import User

class StaticViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ['home', 'contact', 'book_lesson', 'student_dashboard', 'teacher_dashboard',
                'checkout_success', 'checkout_error', 'view_bag']

    def location(self, item):
        return reverse(item)


class UserProfileSitemap(Sitemap):
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        return User.objects.filter(profile__is_teacher=True)

    def location(self, obj):
        return reverse('teacher_profile', args=[obj.id])
