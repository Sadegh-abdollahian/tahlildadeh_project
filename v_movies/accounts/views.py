from django.shortcuts import render
from .serialiazers import RegisterSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.request import Request


# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request: Request):
        data = request.data

        serialiazer = self.serializer_class(data=data)

        if serialiazer.is_valid():
            serialiazer.save()

            response = {"message": "User created successfuly", "data": serialiazer.data}

            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(data=serialiazer.errors, status=status.HTTP_400_BAD_REQUEST)
