import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VerEpisodioComponent } from './ver-episodio.component';

describe('VerEpisodioComponent', () => {
  let component: VerEpisodioComponent;
  let fixture: ComponentFixture<VerEpisodioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VerEpisodioComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VerEpisodioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
