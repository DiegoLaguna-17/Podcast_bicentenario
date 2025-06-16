import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListEpListaComponent } from './list-ep-lista.component';

describe('ListEpListaComponent', () => {
  let component: ListEpListaComponent;
  let fixture: ComponentFixture<ListEpListaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListEpListaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListEpListaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
