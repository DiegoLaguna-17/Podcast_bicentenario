import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionPodcastsComponent } from './gestion-podcasts.component';

describe('GestionPodcastsComponent', () => {
  let component: GestionPodcastsComponent;
  let fixture: ComponentFixture<GestionPodcastsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GestionPodcastsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestionPodcastsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
