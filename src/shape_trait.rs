use parry3d::shape;
pub trait ShapeTrait {
  fn get_inner(&self) -> &dyn shape::Shape;
}
