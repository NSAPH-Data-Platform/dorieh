package org.forome.dorieh.domain

import org.forome.dorieh.dsl.Dataflow


class Workflow extends Base
{
  String name
  String description
  String domain
  String goal

  def methodMissing(String name, Object args)
  {
    switch (name) {
      case "build":
        goal = currentContext.get ("name")
        return
      case "domain":
        domain = currentContext.get ("name")
        return 
    }
    currentContext = [
            name: name,
            closure: args[0]
    ]
  }

  public void domain(String arg)
  {
    domain = arg
  }

  public void build(String arg)
  {
    goal = arg
  }

}
