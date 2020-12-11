import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { GoogleLoginComponent } from './google-login/google-login.component';
import {SocialLoginModule, SocialAuthServiceConfig} from "angularx-social-login";
import {GoogleLoginProvider} from "angularx-social-login";
import { FullCalendarModule } from '@fullcalendar/angular';
import dayGridPlugin from '@fullcalendar/daygrid';
import interactionPlugin from '@fullcalendar/interaction';
import listPlugin from '@fullcalendar/list';
import timeGridPlugin from '@fullcalendar/timegrid';
import { UserCalendarComponent } from './user-calendar/user-calendar.component';
import { UserActivityComponent } from './user-activity/user-activity.component';
import { MonplanyChatbotComponent } from './monplany-chatbot/monplany-chatbot.component';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule} from "@angular/forms";

FullCalendarModule.registerPlugins([ // register FullCalendar plugins
  dayGridPlugin,
  timeGridPlugin,
  listPlugin,
  interactionPlugin
]);

@NgModule({
  declarations: [
    AppComponent,
    GoogleLoginComponent,
    UserCalendarComponent,
    UserActivityComponent,
    MonplanyChatbotComponent,
    /*UserCalendarComponent,*/
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    /*CalendarModule.forRoot({ provide: DateAdapter, useFactory: adapterFactory }),*/
    SocialLoginModule,
    FullCalendarModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [
    {
      provide: 'SocialAuthServiceConfig',
      useValue: {
        autoLogin: true,
        providers: [
          {
            id: GoogleLoginProvider.PROVIDER_ID,
            provider: new GoogleLoginProvider(
              '1062107119819-3q63e96rqqg0ugu8rhd94j5lfmrdu121.apps.googleusercontent.com'
            )
          }
        ]
      } as SocialAuthServiceConfig,
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
