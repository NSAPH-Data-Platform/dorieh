package org.forome.dorieh.domain


class ListCollector
{
  List<String> items = []

  def methodMissing(String name, args) {
    if (name == "item") {
      for (def arg: args)
        items << arg
    } else {
        items << name
    }
  }

  List<String> getItems() {
    return items
  }

}
