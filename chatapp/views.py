from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Room, Message
from .forms import MessageForm  # Import the Message form for handling messages with files
from .chatbot import get_bot_response  # Import the chatbot function
import json

# Signup view to handle user registration
def signup(request):
    """View to handle user signup."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('rooms')  # Redirect to rooms page after successful signup
    else:
        form = UserCreationForm()
    
    return render(request, 'signup.html', {'form': form})

@login_required
def rooms(request):
    """View to list all available rooms."""
    all_rooms = Room.objects.all()  # Get all rooms to display
    return render(request, 'rooms.html', {'rooms': all_rooms})

@login_required
def room(request, slug):
    """View to handle chat within a specific room, including bot responses."""
    room = get_object_or_404(Room, slug=slug)  # Fetch the room or return 404 if not found
    messages = Message.objects.filter(room=room).order_by('created_on')  # Fetch messages in order
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        
        if form.is_valid():
            content = form.cleaned_data['content']
            file = form.cleaned_data['file']
            
            # Check if the message is directed to the bot
            if content and content.lower().startswith('bot:'):
                user_message = content[4:].strip()  # Remove "bot:" from the message
                bot_response = get_bot_response(user_message)  # Get bot response
                
                # Save the bot's response as a message in the room
                Message.objects.create(
                    room=room,
                    user=None,  # Optionally, use a bot user for distinction
                    content=f"Bot: {bot_response}",  # Prefix bot's response with "Bot:"
                )
                return redirect('chat_room', slug=slug)  # Redirect back to room to show bot response

            # Handle regular messages (either text or file)
            new_message = form.save(commit=False)
            new_message.user = request.user
            new_message.room = room
            new_message.save()
            return redirect('chat_room', slug=slug)  # Redirect to update with the new message

    else:
        form = MessageForm()  # Empty form for GET requests

    return render(request, 'room.html', {
        'room_name': room.name,
        'room': room,
        'messages': messages,
        'form': form,  # Pass the form to the template
    })

# Chatbot response endpoint for AJAX chatbot functionality
@csrf_exempt
def chatbot_response(request):
    """Handle chatbot responses for AJAX requests."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            if user_message:
                bot_response = get_bot_response(user_message)
                return JsonResponse({'response': bot_response})
            else:
                return JsonResponse({'response': 'Please provide a valid message.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'response': 'Invalid JSON format.'}, status=400)
    return render(request, 'chatbot.html')  # Render chatbot page for GET requests

# Video signaling endpoint for WebRTC
@csrf_exempt
def video_signal(request):
    """Handle signaling data for WebRTC video calls."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Handle WebRTC offer, answer, and ICE candidate signaling here
            return JsonResponse(data)  # For now, simply echo back the signaling data
        except json.JSONDecodeError:
            return JsonResponse({'response': 'Invalid JSON format.'}, status=400)

    return JsonResponse({'response': 'Invalid request method.'}, status=400)
