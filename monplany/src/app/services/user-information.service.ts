import { Injectable } from '@angular/core';
import {CalendarEvent} from "../user-calendar/calendar-event";

@Injectable({
  providedIn: 'root'
})
export class UserInformationService {

  email: string;
  name: string = 'user';
  calendarEvents: CalendarEvent[];

  constructor() { }
}
