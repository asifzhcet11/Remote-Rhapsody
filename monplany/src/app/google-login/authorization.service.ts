import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {AuthenticatedUser} from "./authenticated-user";
import {UserIdToken} from "./user-id-token";

@Injectable({
  providedIn: 'root'
})
export class AuthorizationService {

  SAVE_CREDENTIALS_URL: string = "http://127.0.0.1:5000/monplany/calendar/creds/save";

  constructor(private http: HttpClient) { }

  saveAuthorizationCode(user: AuthenticatedUser){
    return this.http.post<UserIdToken>(
      this.SAVE_CREDENTIALS_URL,
      user,
      {
        headers: new HttpHeaders({'X-Requested-With': 'XMLHttpRequest',
                                  'Access-Control-Allow-Headers': 'Content-Type',
                                  'Access-Control-Allow-Methods': 'POST',
                                  'Access-Control-Allow-Origin': '*'})

      });
  }
}
