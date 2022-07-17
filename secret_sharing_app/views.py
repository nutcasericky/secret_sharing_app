from django.shortcuts import render, redirect


# Create your views here.
def secret(request):
    if request.method == "POST":
        secret = request.POST.get("secret")
        #participant_no = request.POST.get("number_of_participants")
        #shares_no = request.POST.get("number_of_shares")
        print(secret)

    return render(request, "secret.html", )

