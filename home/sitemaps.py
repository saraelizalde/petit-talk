from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from userprofile.models import User


class StaticViewSitemap(Sitemap):
    """
    Sitemap for static views that do not rely on database models.

    This sitemap includes pages such as the homepage, contact page,
    dashboards, and checkout result pages. URLs are resolved using
    Django's URL names via `reverse()`.

    Attributes:
        priority (float): Importance of the pages for search engines.
        changefreq (str): Expected frequency of page content changes.
    """
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        """
        Return a list of URL names to include in the sitemap.

        Returns:
            list[str]: A list of named URL patterns.
        """
        return ['home', 'contact', 'book_lesson',
                'student_dashboard', 'teacher_dashboard',
                'checkout_success', 'checkout_error', 'view_bag'
                ]

    def location(self, item):
        """
        Resolve each URL name to its actual path.

        Args:
            item (str): The URL name.

        Returns:
            str: The resolved URL path.
        """
        return reverse(item)


class UserProfileSitemap(Sitemap):
    """
    Sitemap for teacher profile pages.

    Includes only users whose related profile is marked as `is_teacher=True`.
    Each profile appears at the URL for the teacher profile page.

    Attributes:
        priority (float): Page importance for SEO crawlers.
        changefreq (str): Likely frequency of profile updates.
    """
    priority = 0.6
    changefreq = 'monthly'

    def items(self):
        """
        Return a queryset of users who are teachers.

        Returns:
            QuerySet[User]: Users with associated teacher profiles.
        """
        return User.objects.filter(profile__is_teacher=True)

    def location(self, obj):
        """
        Return the URL for the teacher profile page.

        Args:
            obj (User): The user instance to generate a URL for.

        Returns:
            str: The URL to the teacher's public profile.
        """
        return reverse('teacher_profile', args=[obj.id])
