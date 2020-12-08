import {Component} from '@angular/core';
import {CalendarView, CalendarEvent, CalendarEventTimesChangedEvent} from "angular-calendar";
import { Subject } from 'rxjs';
import {startOfDay, endOfDay, subDays, addDays, endOfMonth, isSameDay, isSameMonth, addHours,} from 'date-fns';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  /*title = 'monplany';
  view: CalendarView = CalendarView.Month;
  calendarView = CalendarView;
  viewDate: Date = new Date();
  events: CalendarEvent[] = [];
  activeDayIsOpen: boolean = true;
  refresh: Subject<any> = new Subject();

  changeView(view: CalendarView){
    this.view = view;
  }

  dayClicked({ date, events }: { date: Date; events: CalendarEvent[] }): void {
    if (isSameMonth(date, this.viewDate)) {
      this.activeDayIsOpen = !((isSameDay(this.viewDate, date) && this.activeDayIsOpen === true) ||
        events.length === 0);
      this.viewDate = date;
    }
  }

  handleEvent(action: string, event: CalendarEvent): void {
    console.log("handled event");
  }

  eventTimesChanged({
                      event,
                      newStart,
                      newEnd,
                    }: CalendarEventTimesChangedEvent): void {
    this.events = this.events.map((iEvent) => {
      if (iEvent === event) {
        return {
          ...event,
          start: newStart,
          end: newEnd,
        };
      }
      return iEvent;
    });
    this.handleEvent('Dropped or resized', event);
  }

  closeOpenMonthViewDay() {
    this.activeDayIsOpen = false;
  }*/
}
