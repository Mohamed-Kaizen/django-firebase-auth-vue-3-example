from typing import Dict, Tuple
from django.db import IntegrityError
from firebase_admin import auth
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import FireBaseAuthSerializer


class FireBaseAuthAPI(GenericAPIView):
    serializer_class = FireBaseAuthSerializer

    def post(
        self: "FireBaseAuthAPI", 
        request: Request, 
        *args: Tuple, 
        **kwargs: Dict
    ) -> Response:
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            id_token = serializer.data.get('token')

            try:
                decoded_token = auth.verify_id_token(id_token)

            except ValueError:
                raise APIException(
                    detail='Invalid token',
                    code=status.HTTP_400_BAD_REQUEST
                )

            try:
                firebase_user_id = decoded_token['user_id']

            except KeyError:
                raise APIException(
                    detail='The user provided with the auth token is not a valid Firebase user, it has no Firebase UID',
                    code=status.HTTP_400_BAD_REQUEST
                )

            try:
                user = CustomUser.objects.get(firebase_user_id=firebase_user_id)

                content = {
                    "username": user.username,
                    "email": user.email,
                    "firebase_user_id": user.firebase_user_id
                }

                return Response(content, status=status.HTTP_200_OK)

            except CustomUser.DoesNotExist:
                user = auth.get_user(firebase_user_id)

                try:
                    new_user = CustomUser.objects.create(
                        username=user.display_name,
                        email=user.email,
                        firebase_user_id=firebase_user_id
                    )

                    content = {
                        "username": new_user.username,
                        "email": new_user.email,
                        "firebase_user_id": new_user.firebase_user_id
                    }

                    return Response(content, status=status.HTTP_201_CREATED)

                except IntegrityError:
                    raise APIException(
                        detail='A user with the provided Firebase UID already exists',
                        code=status.HTTP_400_BAD_REQUEST
                    )



@api_view()
def public(request: Request) -> Response:
    return Response({"message": "Hello,  User X"})


@api_view()
@permission_classes([IsAuthenticated])
def protected(request: Request) -> Response:
    return Response({"message": f"Hello,  {request.user}"})
