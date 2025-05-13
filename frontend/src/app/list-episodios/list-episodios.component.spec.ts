import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListEpisodiosComponent } from './list-episodios.component';

describe('ListEpisodiosComponent', () => {
  let component: ListEpisodiosComponent;
  let fixture: ComponentFixture<ListEpisodiosComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListEpisodiosComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListEpisodiosComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
