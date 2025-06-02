import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListReseniaComponent } from './list-resenia.component';

describe('ListReseniaComponent', () => {
  let component: ListReseniaComponent;
  let fixture: ComponentFixture<ListReseniaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListReseniaComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListReseniaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
