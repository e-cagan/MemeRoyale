from rest_framework import serializers
from .models import User, Room, Round, Meme, Vote

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# Room Serializer
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

    def create(self, validated_data):
        room = Room.objects.create(**validated_data)
        return room

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# Round Serializer
class RoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Round
        fields = '__all__'


# Meme Serializer
class MemeSerializer(serializers.ModelSerializer):
    total_votes = serializers.ReadOnlyField()

    class Meta:
        model = Meme
        fields = '__all__'

    def create(self, validated_data):
        meme = Meme.objects.create(**validated_data)
        return meme

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


# Vote Serializer
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

    def create(self, validated_data):
        meme = validated_data.get('meme')
        voter = validated_data.get('voter')

        # Kullanıcı aynı meme için daha önce oy verdiyse, yeni oy eklememeliyiz
        existing_vote = Vote.objects.filter(meme=meme, voter=voter).first()
        if existing_vote:
            raise serializers.ValidationError("You have already voted for this meme.")
        
        return super().create(validated_data)
