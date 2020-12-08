import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MonplanyChatbotComponent } from './monplany-chatbot.component';

describe('MonplanyChatbotComponent', () => {
  let component: MonplanyChatbotComponent;
  let fixture: ComponentFixture<MonplanyChatbotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MonplanyChatbotComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MonplanyChatbotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
