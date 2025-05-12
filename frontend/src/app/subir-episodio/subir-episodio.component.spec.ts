import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SubirEpisodioComponent } from './subir-episodio.component';

describe('SubirEpisodioComponent', () => {
  let component: SubirEpisodioComponent;
  let fixture: ComponentFixture<SubirEpisodioComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SubirEpisodioComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SubirEpisodioComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
