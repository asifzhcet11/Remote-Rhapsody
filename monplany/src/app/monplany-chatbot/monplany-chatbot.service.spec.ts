import { TestBed } from '@angular/core/testing';

import { MonplanyChatbotService } from './monplany-chatbot.service';

describe('MonplanyChatbotService', () => {
  let service: MonplanyChatbotService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MonplanyChatbotService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
