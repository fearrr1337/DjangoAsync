from django.core.exceptions import PermissionDenied


class PolicyMixin:
    policy_class = None
    policy_action = None

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        policy = self.policy_class(request.user, obj)

        if not getattr(policy, self.policy_action)():
            raise PermissionDenied("У вас нет прав")

        return super().dispatch(request, *args, **kwargs)