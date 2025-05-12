import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PodcastCardComponent } from './podcast-card.component';

describe('PodcastCardComponent', () => {
  let component: PodcastCardComponent;
  let fixture: ComponentFixture<PodcastCardComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PodcastCardComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PodcastCardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
