import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GestionEpisodiosComponent } from './gestion-episodios.component';

describe('GestionEpisodiosComponent', () => {
  let component: GestionEpisodiosComponent;
  let fixture: ComponentFixture<GestionEpisodiosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GestionEpisodiosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GestionEpisodiosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
