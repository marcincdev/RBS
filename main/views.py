from django.db.models import Q
from main.models import Room, Booking
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views import View
from django.shortcuts import render, get_object_or_404
from datetime import date


class CalendarView(ListView):
    model = Booking
    template_name = 'main/calendar.html'


# class RoomListView(ListView):  # Generic list view
#     model = Room
#     ordering = ['-capacity']


class MyRoomListView(View):  
    template_name = 'main/room_list.html'

    def get(self, request):  # That the solution was inspired by the Igor Sulim -> https://github.com/isulim/Warsztat_3
        room_list = Room.objects.all().order_by('-capacity')
        available = ''
        today_str = date.today().strftime("%Y-%m-%d")
        for room in room_list:
            if (date.today(),) in room.booking_set.filter(date__gte=date.today()).values_list('date'):
                available = 'Booked'
            else:
                available = 'Free'
            room.available = available
        return render(request, self.template_name, locals())


class RoomDetailView(DetailView):
    model = Room


class RoomUpdateView(UpdateView):
    model = Room
    fields = '__all__'
    template_name = 'main/room_form.html'
    success_url = reverse_lazy('room-list')


class RoomDeleteView(DeleteView):
    model = Room
    template_name = 'main/room_confirm_delete.html'
    success_url = reverse_lazy('room-list')


class RoomCreateView(CreateView):
    model = Room
    fields = '__all__'
    template_name = 'main/room_form.html'
    success_url = reverse_lazy('room-list')


class BookingCreateView(CreateView):
    model = Booking
    fields = '__all__'
    template_name = 'main/booking_form.html'
    success_url = reverse_lazy('room-list')


class SearchRoomView(ListView):
    model = Room
    #template_name = "products/list.html"

    def get_queryset(self, *args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q', None) # method_dict['q']
        print(query)
        if query is not None:
            lookups = Q(name__icontains = query) | Q(capacity__icontains = query)
            return Room.objects.filter(lookups).distinct()
        return Room.objects.all().order_by('-capacity')

        # __icontains = field contains this
        #__iexact = fields is exactly this

