import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PaginaPodcastComponent } from './pagina-podcast.component';

describe('PaginaPodcastComponent', () => {
  let component: PaginaPodcastComponent;
  let fixture: ComponentFixture<PaginaPodcastComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PaginaPodcastComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PaginaPodcastComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
