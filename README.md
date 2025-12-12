# Software-House-task
Django_full_stack_position
## When migrate database, run these commands in shell_plus
CustomUser.objects.create(email="user@user.com", role=UserRole.admin)
user = CustomUser.objects.get(pk=1)
user.set_password("password")
user.save()


