from django.conf import settings

def get_git_info(request):
    return {
        'GIT_REPO_LINK': f"{settings.GIT_REPO}/tree/{settings.GIT_TAG if settings.GIT_TAG else settings.GIT_COMMIT}",
        'GIT_REPO_LINK_TEXT': f"GitHub{' ' + settings.GIT_TAG if settings.GIT_TAG else ''}",
    }