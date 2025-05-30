import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListCreadoresComponent } from './list-creadores.component';

describe('ListCreadoresComponent', () => {
  let component: ListCreadoresComponent;
  let fixture: ComponentFixture<ListCreadoresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListCreadoresComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListCreadoresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
