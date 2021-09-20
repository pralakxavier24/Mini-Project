from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib import messages
from .models import user_Action_Detail
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


@api_view(["GET"])
def index(request):
    if request.method == "GET":
        data = []
        objs = user_Action_Detail.objects.all()

        for i in objs:
            temp = {
                "id": f"{i.id}",
                "user": f"{i.user}",
                "Desc": f"{i.p_desc}",
                "Pic": f"{i.p_pic}",
                "Heading": f"{i.p_heading}"
            }
            data.append(temp)
        return Response({"message":f"{data}"}, status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def login(request):
    if request.method == "POST":
        username = request.data["username"]
        password = request.data["password"]

        user = User.objects.get(username=username)
        if user.check_password(password):
            return Response({"message": "Login Successful"},status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register(request):
    if request.method == "POST":
        username = request.data["username"]
        password = request.data["password"]
        email = request.data["email"]

        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        return Response({"message": f"User registered successfully"},status=status.HTTP_202_ACCEPTED)

class user_Details(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id=None):
        data = []
        if id is None:
            objs = user_Action_Detail.objects.filter(user=request.user)
            for i in objs:
                temp = {
                    "id": f"{i.id}",
                    "Desc": f"{i.p_desc}",
                    "Pic": f"{i.p_pic}",
                    "Heading": f"{i.p_heading}"
                }
                data.append(temp)
        else:
            objs = user_Action_Detail.objects.get(id=id)
            temp = {
                "id": f"{objs.id}",
                "Desc": f"{objs.p_desc}",
                "Pic": f"{objs.p_pic}",
                "Heading": f"{objs.p_heading}"
            }
            data.append(temp)

        return Response({"data": f"{data}"},status=status.HTTP_200_OK)

    def post(self, request):
        data = []
        p_desc = request.data["p_desc"]
        p_pic = request.data["p_pic"]
        p_heading = request.data["p_heading"]

        seri, created = user_Action_Detail.objects.get_or_create(user=request.user, p_desc=p_desc, p_pic=p_pic,
                                                                 p_heading=p_heading)
        new = {
            "Desc": f"{seri.p_desc}",
            "Pic": f"{seri.p_pic}",
            "Heading": f"{seri.p_heading}"
        }
        data.append(new)
        if created:
            return Response({"message": f"{data}"}, status=status.HTTP_201_CREATED)
        return Response({"message": "Unable to create a post"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, id=None):
        data = []
        p_desc = request.data["p_desc"]
        p_pic = request.data["p_pic"]
        p_heading = request.data["p_heading"]

        try:
            seri = user_Action_Detail.objects.get(id=id)

            seri.p_desc = p_desc
            seri.p_pic = p_pic
            seri.p_heading = p_heading
            seri.save()

            new = {
                "Desc": f"{seri.p_desc}",
                "Pic": f"{seri.p_pic}",
                "Heading": f"{seri.p_heading}"
            }
            data.append(new)
            return Response({"message": f"post updated successfully - {data}"}, status=status.HTTP_202_ACCEPTED)

        except Exception:
            return Response({"message": "Try again"}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            seri = user_Action_Detail.objects.get(user=request.user, id=id)

        except Exception:
            return Response({"message": "User details not found"}, status=status.HTTP_400_BAD_REQUEST)

        seri.delete()
        return Response({"message": "post deleted successfully"}, status=status.HTTP_200_OK)
