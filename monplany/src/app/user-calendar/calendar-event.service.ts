import { Injectable } from '@angular/core';
import {UserInformationService} from "../services/user-information.service";
import {HttpClient, HttpHeaders, HttpParams} from "@angular/common/http";
import {CalendarEvent} from "./calendar-event";

@Injectable({
  providedIn: 'root'
})
export class CalendarEventService {

  CALENDAR_TODAY_EVENT_GET = "http://127.0.0.1:5000/monplany/calendar/events";

  constructor(private userInformationService: UserInformationService,
              private http: HttpClient) { }

  getTodayEvents(){
    return this.http.get<CalendarEvent[]>(this.CALENDAR_TODAY_EVENT_GET, {
        headers: new HttpHeaders({'Access-Control-Allow-Headers': 'Content-Type',
                  'Access-Control-Allow-Methods': 'POST',
                  'Access-Control-Allow-Origin': '*'}),
        params: new HttpParams().set('email', this.userInformationService.email)
      });
  }
}
