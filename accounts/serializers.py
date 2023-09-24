from rest_framework import serializers
from .models import Organization,JobSeeker
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password','first_name','last_name']
        extra_kwargs = {
            'password' : {'write_only': True},
            'id':{'read_only':True}
        }
    
class JobSeekerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    lastname = serializers.CharField(source='user.last_name')  

    firstname = serializers.CharField(source='user.first_name')  
    password=serializers.CharField(source='user.password',write_only=True,style={'input_type': 'password'})

    class Meta:
        model = JobSeeker
        fields=['id','username', 'email', 'password','firstname','lastname','description','no_of_years_experience','phone_number','resume','skills']
        extra_kwargs = {
            # 'skills':{'read_only':True}
            'id':{'read_only':True}

        }
    def create(self, validated_data):
        data= validated_data
        if User.objects.filter(email=data['user']['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        if User.objects.filter(username=data['user']['username']).exists():
            raise serializers.ValidationError({'error': 'Username already exists!'})
        
        user=User(username=data['user']['username'],email=data['user']['email'],
                  first_name=data['user']['first_name'],last_name=data['user']['last_name']
                  )
        user.set_password(data['user']['password'])

        jobseeker=JobSeeker(description=data['description'],phone_number=data['phone_number'],
                            no_of_years_experience=data['no_of_years_experience'],
                            resume=data['resume'],skills=data['skills'])
        jobseeker.user=user
        user.save()

        jobseeker.save()

        return jobseeker
    
    
    
    
class OrganizationSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')  
    password=serializers.CharField(source='user.password',write_only=True)
    
    class Meta:
        model = Organization
        fields = [ 'id','username', 'email', 'password','location','name','website','overview','founded_at']
        extra_kwargs = {
            # 'skills':{'read_only':True}
            'id':{'read_only':True}

        }
        # exclude=['id']
        
    def create(self, validated_data):
        data= validated_data
       
        if User.objects.filter(email=data['user']['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})
        if User.objects.filter(username=data['user']['username']).exists():
            raise serializers.ValidationError({'error': 'Username already exists!'})
        user=User(username=data['user']['username'],email=data['user']['email'])
        user.set_password(data['user']['password'])
        user.save()
        
        organization= Organization(name=data['name'],founded_at=data['founded_at'],overview=data['overview'],
                          location=data['location'],website=data['website'])

       
        # user=
        # user_vd = validated_data.pop('user')
        # organization = Organization(**validated_data)
        # organization.save()

        # print(validated_data)
        # user= User.objects.create(user_vd)
        organization.user = user
        organization.save()

        return organization
    
    
    # def create(self, validated_data):
    #     # Separate user data from the organization data
    #     # user_data = validated_data.pop('user')
        
    #     # Create the User object
    #     password = user_data.pop('password')
    #     user = User(**user_data)
    #     user.set_password(password)
    #     user.save()
        
    #     # Create the associated Organization object
    #     organization = Organization(**validated_data, user=user)
    #     organization.save()
        
        # return organization
# class OrganizationSerializer(serializers.ModelSerializer):
    
# class OrganizationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model=Organization
#         fields='__all__'
        
        
# class UserSerializer(serializers.ModelSerializer):
#     website= serializers.CharField(source='organization.website')
#     overview= serializers.CharField(source='organization.overview')
#     founded_at= serializers.CharField(source='organization.founded_at')
#     location= serializers.CharField(source='organization.location')


#     class Meta:
#         model = User
#         fields=['id','username','email','password','location','website','overview','founded_at']
#         # fields='__all__'
#         extra_kwargs = {
#             'password' : {'write_only': True},
#             'id':{'read_only':True}
#         }
        
#     def save(self):
#         password = self.validated_data['password']
#         account = User(email=self.validated_data['email'], username=self.validated_data['username'])
        
#         account.set_password(password)
#         account.save()
#         profile=Organization(user=account,website=self.validated_data['organization']['website'],
#                              overview=self.validated_data['organization']['overview'],
#                              founded_at=self.validated_data['organization']['founded_at'],
#                              location=self.validated_data['organization']['location'])
#         profile.save()

#         return account