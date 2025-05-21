import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardReseniasComponent } from './card-resenias.component';

describe('CardReseniasComponent', () => {
  let component: CardReseniasComponent;
  let fixture: ComponentFixture<CardReseniasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CardReseniasComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CardReseniasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
