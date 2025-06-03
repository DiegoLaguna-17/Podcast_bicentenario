import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubirPodcastComponent } from './subir-podcast.component';

describe('SubirPodcastComponent', () => {
  let component: SubirPodcastComponent;
  let fixture: ComponentFixture<SubirPodcastComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubirPodcastComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubirPodcastComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
