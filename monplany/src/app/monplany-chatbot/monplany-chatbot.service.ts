import { Injectable } from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";

@Injectable({
  providedIn: 'root'
})
export class MonplanyChatbotService {

  CHATBOT_URL: string = "http://127.0.0.1:5000/monplany/chatbot";

  constructor(private http: HttpClient) { }

  recieve(){
    return this.http.get(this.CHATBOT_URL,
      {
        headers: new HttpHeaders({'X-Requested-With': 'XMLHttpRequest',
          'Access-Control-Allow-Headers': 'Content-Type',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Origin': '*'})

      });
  }
}
