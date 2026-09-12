package org.forome.dorieh.dsl

class DSLScript extends Script {
  Dataflow dsl = new Dataflow() // automatically injects a Dataflow instance

  @Override
  Object run() {
    // By having this, every method in your script will be treated as dsl.whateverMethod()
    return runScriptWithContext()
  }

  private Object runScriptWithContext() {
    dsl.with {
      this.getBinding().variables.each { k, v -> this.setProperty(k, v) } // inject all variables
      return this.runClosure(this) // Execute the script body
    }
  }

  private Object runClosure(DSLScript dslScriptBase) {
    Object result = dslScriptBase.run()
    return result
  }

  def methodMissing(String name, args) {
    dsl.invokeMethod(name, args)
  }

  // Intercept any unresolved property access in the script and delegate to dsl
  def propertyMissing(String name) {
    return dsl.getProperty(name)
  }

  def propertyMissing(String name, value) {
    dsl.setProperty(name, value)
  }

}