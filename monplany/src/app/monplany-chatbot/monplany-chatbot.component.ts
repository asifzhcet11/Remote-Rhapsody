import { Component, OnInit } from '@angular/core';
import {UserInformationService} from "../services/user-information.service";
import {MonplanyMessage} from "./monplany-message";
import {MonplanyChatbotService} from "./monplany-chatbot.service";

@Component({
  selector: 'app-monplany-chatbot',
  templateUrl: './monplany-chatbot.component.html',
  styleUrls: ['./monplany-chatbot.component.css']
})
export class MonplanyChatbotComponent implements OnInit {

  messages: MonplanyMessage[] = [];
  constructor(private userInformationService: UserInformationService,
              private monplanyChatbotService: MonplanyChatbotService) { }

  ngOnInit(): void {
    this.messages.push({
      text: "Hallo, ich bin MonPlany! Ich bin hier, um Ihnen zu helfen, Ihren Tag effizient zu planen.",
      fromSelf: false
    });


    this.monplanyChatbotService.recieve().subscribe(responseData => {
      if (responseData.hasOwnProperty('text'))
        this.messages.push({
          text: responseData['text'],
          fromSelf: false
        })

      }

    })
  }
}
