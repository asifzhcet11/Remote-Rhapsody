import {Component, OnInit, ViewChild} from '@angular/core';

import {
  CalendarOptions,
  DateSelectArg,
  EventClickArg,
  EventApi,
  CalendarOptionRefiners,
  FullCalendarComponent
} from '@fullcalendar/angular';
import {CalendarEventService} from "./calendar-event.service";
import {UserInformationService} from "../services/user-information.service";
import {UserCalendarColorConfig} from "./user-calendar-color-config";

@Component({
  selector: 'app-user-calendar',
  templateUrl: './user-calendar.component.html',
  styleUrls: ['./user-calendar.component.css']
})
export class UserCalendarComponent implements OnInit {

  @ViewChild('calendar') calendarComponent: FullCalendarComponent;

  calendarOptions: CalendarOptions = {
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'dayGridMonth,timeGridWeek,timeGridDay'
    },
    buttonText:{
      today:    'Today',
      month:    'Month',
      week:     'Week',
      day:      'Day',
    },
    themeSystem: 'bootstrap',
    initialView: 'dayGridMonth',
    nowIndicator: true,
    weekends: true,
    editable: true,
    selectable: true,
    selectMirror: true,
    dayMaxEvents: true,
    select: this.handleDateSelect.bind(this),
    eventClick: this.handleEventClick.bind(this),
    eventsSet: this.handleEvents.bind(this),
    /* you can update a remote database when these fire:
    eventAdd:
    eventChange:
    eventRemove:
    */
    events: []
  };

  constructor(private calendarEventService: CalendarEventService,
              private userInformationService: UserInformationService) {

  }

  ngOnInit(): void {}

  handleDateSelect(selectInfo: DateSelectArg){
    console.log("select");
  }
  handleEventClick(clickInfo: EventClickArg){
    console.log("clicked");
  }
  handleEvents(events: EventApi[]){
    console.log(events);
  }

  getEvents(){
    this.calendarEventService.getTodayEvents().subscribe(responseData => {
      this.calendarOptions['events'] = responseData;
    });
  }
}
